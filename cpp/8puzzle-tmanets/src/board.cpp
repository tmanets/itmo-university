#include "board.h"

#include <algorithm>
#include <iostream>
#include <random>
#include <sstream>

Board Board::create_goal(const unsigned size)
{
    unsigned cnt = 1;
    std::vector<std::vector<unsigned>> data;
    data.resize(size, std::vector<unsigned>(size));
    for (unsigned i = 0; i < size; i++) {
        for (unsigned j = 0; j < size; j++) {
            data[i][j] = cnt % (size * size);
            cnt++;
        }
    }
    return Board(data);
}

Board Board::create_random(const unsigned size)
{
    static std::mt19937 rd(std::random_device{}());

    std::vector<unsigned> temp_board(size * size);

    std::iota(temp_board.begin(), temp_board.end(), 0);
    std::shuffle(temp_board.begin(), temp_board.end(), rd);

    std::vector<std::vector<unsigned>> data;
    data.resize(size, std::vector<unsigned>(size));
    for (unsigned i = 0; i < size * size; i++) {
        data[i / size][i % size] = temp_board[i];
    }
    return Board(data);
}

Board::Board(std::vector<std::vector<unsigned>> data)
    : m_data(std::move(data))
{
    find_empty_cell();
}

void Board::find_empty_cell()
{
    for (unsigned i = 0; i < size(); ++i) {
        for (unsigned j = 0; j < size(); ++j) {
            if (!m_data[i][j]) {
                m_empty_cell = {i, j};
                return;
            }
        }
    }
}

unsigned Board::size() const
{
    return m_data.size();
}

bool Board::is_goal() const
{
    return hamming() == 0;
}

unsigned Board::hamming() const
{
    unsigned cost = 0;
    for (unsigned i = 0; i < size(); ++i) {
        for (unsigned j = 0; j < size(); ++j) {
            if (m_data[i][j] != ((1 + i * size() + j) % (size() * size()))) {
                ++cost;
            }
        }
    }
    return cost;
}

unsigned Board::manhattan() const
{
    unsigned cost = 0;

    for (unsigned i = 0; i < size(); i++) {
        for (unsigned j = 0; j < size(); j++) {
            if (m_data[i][j]) {
                cost += abs(static_cast<int>(i - (m_data[i][j] - 1) / size())) +
                        abs(static_cast<int>(j - (m_data[i][j] - 1) % size()));
            }
        }
    }

    return cost;
}

std::string Board::to_string() const
{
    if (size() == 0) {
        return "<empty>";
    }
    std::stringstream string_board;
    for (std::size_t i = 0; i < size(); ++i) {
        for (std::size_t j = 0; j < size(); ++j) {
            string_board << m_data[i][j] << ' ';
        }
        string_board << '\n';
    }
    return string_board.str();
}

bool Board::is_solvable() const
{
    if (is_goal()) {
        return true;
    }
    std::vector<unsigned> row_board;
    row_board.reserve(size() * size());
    for (unsigned i = 0; i < size(); ++i) {
        for (unsigned j = 0; j < size(); ++j) {
            row_board.push_back(m_data[i][j]);
        }
    }
    unsigned inv_count = 0;
    for (unsigned i = 0; i < row_board.size(); ++i) {
        if (row_board[i]) {
            for (unsigned j = i + 1; j < row_board.size(); ++j) {
                if (row_board[j] && row_board[i] > row_board[j]) {
                    inv_count++;
                }
            }
        }
    }

    if (size() % 2) {
        return (inv_count % 2 == 0);
    }
    unsigned pos = size() - m_empty_cell.first;
    if (pos % 2 == 1) {
        return (inv_count % 2 == 0);
    }
    return (inv_count % 2 == 1);
}

std::vector<unsigned> Board::operator[](unsigned int index)
{
    return m_data[index];
}

const std::vector<unsigned> & Board::operator[](unsigned index) const
{
    return m_data[index];
}
std::pair<unsigned, unsigned> Board::get_empty_cell() const
{
    return m_empty_cell;
}
const std::vector<std::vector<unsigned>> & Board::get_board() const
{
    return m_data;
}

std::ostream & operator<<(std::ostream & out, const Board & b)
{
    out << b.to_string();
    return out;
}

bool operator==(const Board & lhs, const Board & rhs)
{
    return lhs.m_data == rhs.m_data;
}
bool operator!=(const Board & lhs, const Board & rhs)
{
    return lhs.m_data != rhs.m_data;
}
