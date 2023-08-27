//
// Created by 49152 on 11.05.2023.
//

#ifndef INC_4X4_GEWINNT_COAPSENDER_H
#define INC_4X4_GEWINNT_COAPSENDER_H


#include "MessageQueue.h"
#include "common.hh"

/**
 * @class CoAPSender
 * @brief Manages the sending of CoAP messages.
 *
 * The CoAPSender handles all operations related to sending messages over 
 * CoAP. It includes functions for sending payload to the server and 
 * handling responses.
 */
class CoAPSender {
public:

    /**
     * @brief Singleton instance pointer.
     */
    static CoAPSender* instance_;

        /**
     * @brief Constructor.
     * 
     * Initializes the CoAPSender with a message queue.
     * 
     * @param queue Reference to the MessageQueue.
     */
    CoAPSender(MessageQueue& queue);

        /**
     * @brief Operator function to process and send messages.
     *
     * Retrieves messages from the queue and sends them using CoAP.
     */
    void operator()();



        /**
     * @brief Response handler for received CoAP messages.
     * 
     * @param session Current CoAP session.
     * @param sent Pointer to the CoAP PDU that was sent.
     * @param received Pointer to the CoAP PDU that was received.
     * @param 
     * @return coap_response_t Response type of the handler.
     */
    static coap_response_t response_handler(coap_session_t *session, 
                                            const coap_pdu_t *sent,
                                            const coap_pdu_t *received,
                                            int);


private:
    MessageQueue& queue_;   ///< Reference to the message queue.
    coap_context_t* ctx;    ///< CoAP context.
    coap_session_t* session;///< CoAP session.
    coap_address_t dst;     ///< CoAP destination address.
    int have_response_;     ///< Flag for received response.

    /**
     * @brief Send payload to CoAP server.
     * 
     * @param payload Payload data to send.
     * @param msg Associated ControllerMessage.
     * @return int Status of the send operation.
     */
    int send_payload_to_server(const char* payload, ControllerMessage msg);
};


#endif //INC_4X4_GEWINNT_COAPSENDER_H
