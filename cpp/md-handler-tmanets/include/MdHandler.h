#pragma once

#include "Packet.h"

#include <chrono>
#include <mutex>
#include <unordered_set>

namespace md_handler {

class IService;

class MdHandler
{
public:
    MdHandler(IService & service);
    void handle_packet(const Packet & packet);
    void handle_resend(const Packet & packet);

private:
    IService & m_service;
    std::mutex m_mutex_queue;
    std::mutex m_mutex;
    std::uint32_t m_next_message = 1;
    std::uint32_t m_last_message = 0;
    std::unordered_set<std::uint32_t> m_packets;
    void handle_queue();
    void enqueue(const Packet & packet);
    static constexpr auto m_sleep_time = std::chrono::milliseconds(100);
};

} // namespace md_handler