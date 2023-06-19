//
// Created by 49152 on 11.05.2023.
//

#include "CoAPSender.h"
#include <iostream>
#include "logging.h"

CoAPSender::CoAPSender(MessageQueue& queue) : queue_(queue) {
    // Your CoAP initialization code goes here
    coap_startup();

    /* Set logging level */
    coap_set_log_level(COAP_LOG_WARN);

    /* resolve destination address where server should be sent */
    //if (resolve_address("localhost", "5683", &dst) < 0) {
    if (resolve_address("192.168.0.104", "5683", &dst) < 0) {
        coap_log_crit("failed to resolve address\n");
        exit(1);
    }

    /* create CoAP context and a client session */
    if (!(ctx = coap_new_context(nullptr))) {
        coap_log_emerg("cannot create libcoap context\n");
        exit(1);
    }

    /* Support large responses */
    coap_context_set_block_mode(ctx,
                                COAP_BLOCK_USE_LIBCOAP | COAP_BLOCK_SINGLE_BODY);

    if (!(session = coap_new_client_session(ctx, nullptr, &dst,
                                            COAP_PROTO_UDP))) {
        coap_log_emerg("cannot create client session\n");
        exit(1);
    }

    coap_register_response_handler(ctx, [](auto, auto,
                                           const coap_pdu_t *received,
                                           auto) {
        //coap_show_pdu(COAP_LOG_WARN, received); //for debugging
        return COAP_RESPONSE_OK;
    });
}

void CoAPSender::operator()() {
    while (true) {
        ControllerMessage msg = queue_.pop();

        if (msg.payload() != 0) {
            logMessage(msg,std::string("PopFromQ"));
            // Convert uint8_t to char*
            char payload[2];
            payload[0] = msg.payload();
            payload[1] = '\0';
            send_payload_to_server(payload,msg);
        }
    }
}


int CoAPSender::send_payload_to_server(const char* payload, ControllerMessage msg) {
    // Your send_payload_to_server code goes here
    coap_pdu_t* pdu = coap_pdu_init(COAP_MESSAGE_NON,
                                    COAP_REQUEST_CODE_POST,
                                    coap_new_message_id(session),
                                    coap_session_max_pdu_size(session));
    if (!pdu) {
        coap_log_emerg("cannot create PDU\n");
        return -1;
    }

    /* add a Uri-Path option */
    coap_add_option(pdu, COAP_OPTION_URI_PATH, 5,
                    reinterpret_cast<const uint8_t *>("hello"));

    coap_add_data(pdu, strlen(payload), reinterpret_cast<const uint8_t *>(payload));

    //coap_show_pdu(COAP_LOG_WARN, pdu);    //for debugging

    logMessage(msg,"SendViaCoap");

    if (coap_send(session, pdu) == COAP_INVALID_MID) {
        coap_log_err("cannot send CoAP pdu\n");
        return -1;
    }

    return 0;
}
