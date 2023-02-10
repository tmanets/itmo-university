#pragma once

#include <algorithm>
#include <iostream>
#include <iterator>
#include <ostream>
#include <stdexcept>
#include <string>
#include <vector>

template <class Key, class Value, class Less = std::less<Key>>
class BPTree
{
    struct Node
    {
        bool leaf = false;
        std::vector<Key> keys;
        std::vector<std::pair<Key, Value>> data;
        Node * parent = nullptr;
        std::vector<Node *> children;
        Node * left = nullptr;
        Node * right = nullptr;

        Node() = default;
    };

    template <class Iter>
    class TreeIterator
    {
    public:
        using difference_type = std::ptrdiff_t;
        using iterator_category = std::forward_iterator_tag;
        using value_type = typename Iter::value_type;
        using reference = typename Iter::reference;
        using pointer = typename Iter::pointer;

        TreeIterator() = default;
        explicit TreeIterator(Node * node)
            : current_node(node)
            , pointer_in_node(node->data.begin())
        {
        }

        explicit TreeIterator(Node * node, size_t pos)
            : current_node(node)
            , pointer_in_node(node->data.begin() + pos)
        {
        }

        explicit TreeIterator(Node * node, Iter it)
            : current_node(node)
            , pointer_in_node(it)
        {
        }

        friend bool operator==(const TreeIterator & lhs, const TreeIterator & rhs)
        {
            return lhs.pointer_in_node == rhs.pointer_in_node;
        }
        friend bool operator!=(const TreeIterator & lhs, const TreeIterator & rhs)
        {
            return lhs.pointer_in_node != rhs.pointer_in_node;
        }
        reference operator*() const
        {
            return *pointer_in_node;
        }
        TreeIterator & operator++()
        {
            ++pointer_in_node;
            if (current_node->right && pointer_in_node == current_node->data.end()) {
                current_node = current_node->right;
                pointer_in_node = current_node->data.begin();
            }
            return *this;
        }
        TreeIterator operator++(int)
        {
            auto tmp = *this;
            operator++();
            return tmp;
        }

        pointer operator->() const
        {
            return pointer_in_node.operator->();
        }

    private:
        Node * current_node;
        Iter pointer_in_node;
    };

    static constexpr std::size_t block_size = 4096;
    static constexpr std::size_t node_size = block_size / (sizeof(Node *) + sizeof(Key));

public:
    using key_type = Key;
    using mapped_type = Value;
    using value_type = std::pair<Key, Value>;
    using reference = value_type &;
    using const_reference = const value_type &;
    using pointer = value_type *;
    using const_pointer = const value_type *;
    using size_type = std::size_t;

    using iterator = TreeIterator<typename std::vector<value_type>::iterator>;
    using const_iterator = TreeIterator<typename std::vector<value_type>::const_iterator>;

    BPTree(std::initializer_list<std::pair<Key, Value>> list)
    {
        insert(list.begin(), list.end());
    }
    BPTree(const BPTree & other)
        : root(copy_node(other.root))
    {
    }
    BPTree(Node & node)
        : root(copy_node(&node))
    {
    }
    BPTree(BPTree && other)
        : root(other.root)
    {
        other.root = nullptr;
    };
    BPTree()
        : root(new Node)
    {
        root->leaf = true;
    };

    ~BPTree()
    {
        clear();
    }

    iterator begin()
    {
        if (root) {
            auto cur = root;
            while (!cur->leaf) {
                cur = cur->children.front();
            }
            return iterator(cur);
        }
        return end();
    }
    const_iterator cbegin() const
    {
        if (root) {
            auto cur = root;
            while (!cur->leaf) {
                cur = cur->children.front();
            }
            return const_iterator(cur);
        }
        return end();
    }
    const_iterator begin() const
    {
        return cbegin();
    }
    iterator end()
    {
        if (!root) {
            return iterator();
        }
        auto cur = root;
        while (!cur->leaf) {
            cur = cur->children.back();
        }
        return iterator(cur, cur->data.end());
    }
    const_iterator cend() const
    {
        if (!root) {
            return const_iterator();
        }
        auto cur = root;
        while (!cur->leaf) {
            cur = cur->children.back();
        }
        return const_iterator(cur, cur->data.end());
    }
    const_iterator end() const
    {
        return cend();
    }

    bool empty() const
    {
        return size() == 0;
    }
    size_type size() const
    {
        return m_size;
    }
    void dfs_clear(Node * node)
    {
        if (!node->leaf) {
            for (auto ch : node->children) {
                dfs_clear(ch);
            }
        }
        delete node;
        return;
    }
    void clear()
    {
        dfs_clear(root);
    }

    size_type count(const Key & key) const
    {
        return contains(key);
    }
    bool contains(const Key & key) const
    {
        return find(key) != cend();
        ;
    }
    iterator lower_bound(const Key & key)
    {
        Node * leaf = find_leaf(key);
        auto it = leaf->data.begin();

        while (it != leaf->data.end() && less(it->first, key)) {
            it++;
        }
        if (it != leaf->data.end()) {
            return iterator(leaf, it);
        }
        if (!leaf->right) {
            return end();
        }
        else {
            return iterator(leaf->right, leaf->right->data.begin());
        }
    }
    const_iterator lower_bound(const Key & key) const
    {
        Node * leaf = find_leaf(key);
        auto it = leaf->data.cbegin();

        while (it != leaf->data.end() && less(it->first, key)) {
            it++;
        }
        if (it != leaf->data.end()) {
            return const_iterator(leaf, it);
        }
        if (!leaf->right) {
            return cend();
        }
        else {
            return const_iterator(leaf->right, leaf->right->data.cbegin());
        }
    }
    iterator upper_bound(const Key & key)
    {
        iterator it = lower_bound(key);
        if (it != end() && it->first == key) {
            return ++it;
        }
        else {
            return it;
        }
    }
    const_iterator upper_bound(const Key & key) const
    {
        const_iterator it = lower_bound(key);
        if (it != cend() && it->first == key) {
            return ++it;
        }
        else {
            return it;
        }
    }

    std::pair<iterator, iterator> equal_range(const Key & key)
    {
        iterator it = find(key);

        if (it == end()) {
            return std::make_pair(end(), end());
        }
        auto next = it;
        ++next;
        return std::make_pair(it, next);
    }
    std::pair<const_iterator, const_iterator> equal_range(const Key & key) const
    {
        auto it = find(key);
        if (it == cend()) {
            return std::make_pair(cend(), cend());
        }
        auto next = it;
        ++next;
        return std::make_pair(it, next);
    }
    // 'at' method throws std::out_of_range if there is no such key
    Value & at(const Key & key)
    {
        iterator it = find(key);
        if (it != end()) {
            return it->second;
        }
        throw std::out_of_range("key not found");
    }
    const Value & at(const Key & key) const
    {
        const_iterator it = find(key);
        if (it != cend()) {
            return it->second;
        }
        throw std::out_of_range("key not found");
    }
    // '[]' operator inserts a new element if there is no such key
    Value & operator[](const Key & key)
    {
        return insert(key, Value()).first->second;
    }
    Value & operator[](Key && key)
    {
        return insert(key, Value()).first->second;
    }
    std::size_t search(Node * leaf, const Key & key)
    {
        size_t pos = 0;
        while (pos < leaf->keys.size() && key > leaf->keys[pos]) {
            ++pos;
        }
        return pos;
    }
    std::pair<iterator, bool> insert(const Key & key, const Value & value)
    {
        Node * leaf = find_leaf(key);
        if (contains(key)) {
            return {find(key), false};
        }
        ++m_size;
        size_t pos = search(leaf, key);
        leaf->keys.insert(leaf->keys.begin() + pos, key);
        leaf->data.insert(leaf->data.begin() + pos, std::make_pair(key, value));
        if (leaf->keys.size() == node_size) {
            split(leaf);
        }

        return {find(key), true};
    }
    template <class ForwardIt>
    void insert(ForwardIt begin, ForwardIt end)
    {
        for (auto it = begin; it != end; ++it) {
            insert(it->first, it->second);
        }
    }
    void insert(std::initializer_list<value_type> list)
    {
        insert(list.begin(), list.end());
    }
    iterator erase(iterator it)
    {
        remove(it->first);
        return it;
    }
    const_iterator erase(const_iterator it)
    {
        remove(it->first);
        return it;
    }

    iterator erase(const_iterator begin, const_iterator end)
    {
        std::vector<Key> to_delete;
        for (auto it = begin; it != end; ++it) {
            to_delete.push_back(it->first);
        }

        for (const auto & key : to_delete) {
            remove(key);
        }
        return lower_bound(to_delete.back());
    }
    size_type erase(const Key & key)
    {
        return remove(key);
    }
    bool remove(const Key & key)
    {
        if (!contains(key)) {
            return false;
        }
        Node * leaf = find_leaf(key);
        --m_size;
        delete_in_node(leaf, key);
        return true;
    }
    iterator find(const Key & key)
    {
        Node * leaf = find_leaf(key);
        for (size_t i = 0; i < leaf->keys.size(); ++i) {
            if (key == leaf->keys[i]) {
                return iterator(leaf, i);
            }
        }

        return end();
    }
    const_iterator find(const Key & key) const
    {
        Node * leaf = find_leaf(key);
        for (size_t i = 0; i < leaf->keys.size(); ++i) {
            if (key == leaf->keys[i]) {
                return const_iterator(leaf, i);
            }
        }
        return cend();
    }

private:
    Node * root;
    size_t m_size = 0;
    Less less;

    Node * find_leaf(const Key & key) const
    {
        auto cur = root;
        if (!cur) {
            return nullptr;
        }
        while (!cur->leaf) {
            Node * next = cur->children.front();

            for (size_t i = 0; i < cur->keys.size(); ++i) {
                if (less(key, cur->keys[i])) {
                    break;
                }
                else {
                    next = cur->children[i];
                }
            }
            cur = next;
        }
        return cur;
    }
    void split(Node * node)
    {
        auto new_node = new Node();
        new_node->left = node;

        if (node->right) {
            new_node->right = node->right;
            node->right->left = new_node;
        }
        node->right = new_node;

        for (size_t i = node_size / 2; i < node_size; ++i) {
            new_node->keys.push_back(node->keys[i]);
            node->keys.pop_back();
        }
        if (node->leaf) {
            new_node->leaf = true;
            for (size_t i = node_size / 2; i < node_size; ++i) {
                new_node->data.push_back(node->data[i]);
                node->data.pop_back();
            }
        }
        else {
            for (size_t i = node_size / 2; i < node_size; ++i) {
                new_node->children.push_back(node->children[i]);
                node->children.pop_back();
                new_node->children.back()->parent = new_node;
            }
        }
        if (root == node) {
            root = new Node();
            node->parent = root;
            new_node->parent = root;
            root->keys.push_back(get_min_key(node));
            root->keys.push_back(get_min_key(new_node));
            root->children.push_back(node);
            root->children.push_back(new_node);
        }
        else {
            auto parent = node->parent;
            new_node->parent = parent;

            Key mid_key = get_min_key(new_node);
            size_t pos = search(parent, mid_key);

            parent->keys.insert(parent->keys.begin() + pos, mid_key);
            parent->children.insert(parent->children.begin() + pos, new_node);

            if (parent->keys.size() == node_size) {
                split(parent);
            }
        }
        update(node);
    }
    void delete_in_node(Node * node, const Key & key)
    {
        update(node);
        if (!node || std::count(node->keys.begin(), node->keys.end(), key) == 0) {
            return;
        }
        size_t pos = search(node, key);
        node->keys.erase(node->keys.begin() + pos);

        if (node->leaf) {
            node->data.erase(node->data.begin() + pos);
        }
        else {
            delete node->children[pos];
            node->children.erase(node->children.begin() + pos);
        }

        if (node != root && node->keys.size() < node_size / 2) {
            Node * left = node->left;
            Node * right = node->right;
            if (left && left->keys.size() > node_size / 2) {

                left->keys.pop_back();
                node->keys.insert(node->keys.begin(), left->keys.back());
                if (left->leaf) {
                    left->data.pop_back();
                    node->data.insert(node->data.begin(), left->data.back());
                }
                else {
                    left->children.pop_back();
                    node->children.insert(node->children.begin(), left->children.back());
                }
                update(node);
                update(left);
            }
            else if (right && right->keys.size() > node_size / 2) {
                right->keys.erase(right->keys.begin());
                node->keys.push_back(right->keys.front());

                if (right->leaf) {
                    right->data.erase(right->data.begin());
                    node->data.push_back(right->data.front());
                }
                else {
                    right->children.erase(right->children.begin());
                    node->children.push_back(right->children.front());
                    node->children.back()->parent = node;
                }
                update(node);
                update(right);
            }
            else if (left && left->parent == node->parent) {
                merge(left, node);
                delete_in_node(left->parent, get_min_key(node));
                update(left);
            }
            else {
                merge(node, right);
                delete_in_node(node->parent, get_min_key(right));
                update(node);
            }
        }
        if (!root->leaf && root->keys.size() == 1 && root->children.front()) {
            root = root->children.front();
            root->parent = nullptr;
        }
    }

    void update(Node * node)
    {
        if (!node) {
            return;
        }
        if (!node->leaf) {
            for (size_t i = 0; i < node->keys.size(); ++i) {
                node->keys[i] = node->children[i]->keys.front();
            }
        }
        update(node->parent);
    }

    void merge(Node * node, Node * right)
    {
        for (size_t i = 0; i < right->keys.size(); ++i) {
            node->keys.push_back(right->keys[i]);
        }
        if (node->leaf) {
            for (size_t i = 0; i < right->keys.size(); ++i) {
                node->data.push_back(right->data[i]);
            }
        }
        else {
            for (size_t i = 0; i < right->keys.size(); ++i) {
                node->children.push_back(right->children[i]);
                node->children.back()->parent = node;
            }
        }

        node->right = right->right;
        if (right->right) {
            right->right->left = node;
        }
        update(right);
    }

    Key get_min_key(Node * cur) const
    {
        if (cur->leaf) {
            return cur->keys.front();
        }
        return get_min_key(cur->children.front());
    }

    Node * copy_node(Node * node_from)
    {
        if (node_from) {
            Node * new_node = new Node(node_from);
            new_node->children = {};
            for (auto child : node_from->children) {
                new_node->children.push_back(copy_node(child));
            }
            return new_node;
        }
        return node_from;
    }
};
