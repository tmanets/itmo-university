#include "MdHandler.h"

#include "IService.h"

#include <thread>

namespace md_handler {

MdHandler::MdHandler(IService & service)
    : m_service(service)
{
}

void MdHandler::enqueue(const Packet & packet)
{
    std::lock_guard<std::mutex> lock(m_mutex_queue);
    for (uint16_t i = 0; i < packet.get_msg_count(); ++i) {
        uint16_t msg = packet.get_seq_num() + i;
        if (msg >= m_next_message) {
            m_packets.insert(msg);
        }
    }
}
void MdHandler::handle_queue()
{
    std::lock_guard<std::mutex> lock(m_mutex_queue);
    while (m_packets.count(m_next_message)) {
        m_packets.erase(m_next_message);
        m_service.handle_message(m_next_message++);
    }
}
void MdHandler::handle_packet(const Packet & packet)
{
    std::unique_lock<std::mutex> lock(m_mutex);
    if (packet.get_msg_count() != 0) {
        enqueue(packet);
        m_last_message = std::max(m_last_message, packet.get_seq_num() + packet.get_msg_count() - 1);
    }
    else {
        m_last_message = std::max(m_last_message, packet.get_seq_num());
    }
    if (m_packets.count(m_next_message)) {
        handle_queue();
    }

    lock.unlock();
    std::this_thread::sleep_for(m_sleep_time);
    lock.lock();

    uint16_t to_resend;
    if (m_packets.empty()) {
        to_resend = m_last_message + 1 - m_next_message;
    }
    else {
        to_resend = *m_packets.begin() - m_next_message;
    }

    if (to_resend > 1) {
        m_service.resend_messages(m_next_message, to_resend);
        std::this_thread::sleep_for(m_sleep_time);
    }
}
void MdHandler::handle_resend(const Packet & packet)
{
    enqueue(packet);
    handle_queue();
}

} // namespace md_handler
