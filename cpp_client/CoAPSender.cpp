//
// Created by 49152 on 11.05.2023.
//

#include "CoAPSender.h"
#include "logging.h"
#include "ConfigReader.h"
#include <iostream>

CoAPSender* CoAPSender::instance_ = nullptr;

CoAPSender::CoAPSender(MessageQueue& queue) : queue_(queue) {
    instance_ = this;
    // Your CoAP initialization code goes here
    coap_startup();

    /* Set logging level */
    coap_set_log_level(COAP_LOG_WARN);

    /* resolve destination address where server should be sent */
    if (resolve_address(ConfigReader::readConfigFile("Server-IP").c_str(), "5683", &dst) < 0) {
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

    // coap_register_response_handler(ctx, [this](auto, auto,
    //                                        const coap_pdu_t *received,
    //                                        auto) {
    //     //coap_show_pdu(COAP_LOG_WARN, received); //for debugging
    //     have_response_ = 1;
    //     return COAP_RESPONSE_OK;
    // });

    coap_register_response_handler(ctx, &CoAPSender::response_handler);

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
            
            have_response_ = 0; // Reset have_response_
            while (have_response_ == 0) {
                coap_io_process(ctx, COAP_IO_WAIT);
            }
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



// //original working repsonse handler
// coap_response_t CoAPSender::response_handler(coap_session_t *session, 
//                                              const coap_pdu_t *sent,
//                                              const coap_pdu_t *received,
//                                              int) {
//     instance_->have_response_ = 1;
//     return COAP_RESPONSE_OK;
// }


//to test response handler
coap_response_t CoAPSender::response_handler(coap_session_t *session, 
                                             const coap_pdu_t *sent,
                                             const coap_pdu_t *received,
                                             int nack_reason) {
    // Getting payload data
    const uint8_t* data = nullptr;
    size_t data_len = 0;
    coap_get_data(received, &data_len, &data);

    if(data_len > 0) {
        // Print payload data as a string (if it's a string)
        std::cout << "Received response: " << std::string((char*)data, data_len) << std::endl;

        // Or, print it as hexadecimal (useful for non-string data)
        for(size_t i = 0; i < data_len; i++)
            printf("%02x", data[i]);
        printf("\n");
    }
    else {
        std::cout << "Received empty response" << std::endl;
    }

    instance_->have_response_ = 1;
    return COAP_RESPONSE_OK;
}


