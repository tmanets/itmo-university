#pragma once

#include <string>
#include <vector>

class Board
{
public:
    static Board create_goal(unsigned size);

    static Board create_random(unsigned size);

    Board() = default;

    explicit Board(std::vector<std::vector<unsigned>> data);

    unsigned size() const;

    bool is_goal() const;

    unsigned hamming() const;

    unsigned manhattan() const;

    std::string to_string() const;

    bool is_solvable() const;

    friend bool operator==(const Board & lhs, const Board & rhs);

    friend bool operator!=(const Board & lhs, const Board & rhs);

    friend std::ostream & operator<<(std::ostream & out, const Board & board);

    std::vector<unsigned> operator[](unsigned index);

    const std::vector<unsigned> & operator[](unsigned index) const;

    std::pair<unsigned, unsigned> get_empty_cell() const;

    const std::vector<std::vector<unsigned>> & get_board() const;

private:
    std::vector<std::vector<unsigned>> m_data;
    std::pair<unsigned, unsigned> m_empty_cell;
    void find_empty_cell();
};
