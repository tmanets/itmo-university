#include "solver.h"

#include <algorithm>
#include <queue>
#include <unordered_map>
#include <unordered_set>

namespace std {
template <>
struct hash<Board>
{
    std::size_t operator()(const Board & board) const
    {
        const std::vector<std::vector<unsigned>> & m_board = board.get_board();
        unsigned seed = m_board.size();
        for (const std::vector<unsigned> & row : m_board) {
            for (const unsigned i : row) {
                seed ^= i + 0x9e3779b9 + (seed << 6) + (seed >> 2);
            }
        }
        return seed;
    }
};
} // namespace std

Solver::Solution Solver::solve(const Board & initial_board)
{
    if (!initial_board.is_solvable()) {
        return Solution();
    }
    if (initial_board.is_goal()) {
        return Solution(initial_board);
    }
    using PathElementPtr = std::shared_ptr<PathElement>;

    static constexpr auto cmp = [](const PathElementPtr & a, const PathElementPtr & b) {
        return a->board.hamming() + a->board.manhattan() > b->board.hamming() + b->board.manhattan();
    };
    std::priority_queue<PathElementPtr, std::vector<PathElementPtr>, decltype(cmp)> queue(cmp);

    std::unordered_set<Board> visited;

    queue.push(std::make_shared<PathElement>(initial_board));

    while (!queue.empty()) {
        auto current = queue.top();
        queue.pop();
        if (current->board.is_goal()) {
            return Solution(current);
        }
        visited.insert(current->board);
        for (const auto & new_board : get_next(current->board)) {
            if (!visited.count(new_board)) {
                queue.push(std::make_shared<PathElement>(new_board, current));
            }
        }
    }

    return Solution();
}

std::vector<Board> Solver::get_next(const Board & board)
{
    auto empty_cell = board.get_empty_cell();
    std::vector<Board> result;
    static constexpr std::array<std::pair<int, int>, 4> offsets = {{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}};
    for (const auto & [x_offset, y_offset] : offsets) {
        size_t x = empty_cell.first + x_offset;
        size_t y = empty_cell.second + y_offset;
        if (x < board.size() && y < board.size()) {
            std::vector<std::vector<unsigned>> data = board.get_board();
            std::swap(data[empty_cell.first][empty_cell.second], data[x][y]);
            result.push_back(Board(data));
        }
    }

    return result;
}

Solver::Solution::Solution(std::shared_ptr<PathElement> current)
{
    unsigned i = current->moves;
    m_moves.resize(i + 1);
    while (current->prev) {
        m_moves[i--] = std::move(current->board);
        current = current->prev;
    }
    m_moves[0] = current->board;
}
