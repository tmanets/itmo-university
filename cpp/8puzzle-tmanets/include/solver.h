#pragma once

#include "board.h"

#include <memory>

class Solver
{
    struct PathElement
    {
        std::shared_ptr<PathElement> prev = nullptr;
        unsigned moves = 0;
        Board board;

        PathElement(const Board & board)
            : board(board)
        {
        }

        PathElement(const Board & board, const std::shared_ptr<PathElement> & prev)
            : prev(prev)
            , board(board)
        {
            moves = prev->moves + 1;
        }
    };

    class Solution
    {
    public:
        Solution() = default;
        Solution(const Board & solution)
            : m_moves({solution})
        {
        }
        Solution(std::shared_ptr<PathElement>);
        std::size_t moves() const { return m_moves.empty() ? 0 : m_moves.size() - 1; }
        using const_iterator = std::vector<Board>::const_iterator;
        const_iterator begin() const { return m_moves.begin(); }

        const_iterator end() const { return m_moves.end(); }

    private:
        std::vector<Board> m_moves;
    };

public:
    static Solution solve(const Board & initial);

private:
    static std::vector<Board> get_next(const Board & current_turn);
};
