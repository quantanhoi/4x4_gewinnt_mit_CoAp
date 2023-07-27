//
// Created by 49152 on 11.05.2023.
//

#ifndef INC_4X4_GEWINNT_COAPSENDER_H
#define INC_4X4_GEWINNT_COAPSENDER_H


#include "MessageQueue.h"
#include "common.hh"

class CoAPSender {
public:
    static CoAPSender* instance_;
    CoAPSender(MessageQueue& queue);
    void operator()();
    static coap_response_t response_handler(coap_session_t *session, 
                                            const coap_pdu_t *sent,
                                            const coap_pdu_t *received,
                                            int);


private:
    MessageQueue& queue_;
    coap_context_t* ctx;
    coap_session_t* session;
    coap_address_t dst;
    int have_response_;

    int send_payload_to_server(const char* payload, ControllerMessage msg);
};


#endif //INC_4X4_GEWINNT_COAPSENDER_H
