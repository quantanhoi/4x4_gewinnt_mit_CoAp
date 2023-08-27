#ifndef INC_4X4_GEWINNT_CONTROLLER_H
#define INC_4X4_GEWINNT_CONTROLLER_H


#include <SDL.h>
#include "ControllerMessage.h"
#include <queue>


/**
 * @class Controller
 * @brief Handles SDL joystick input and manages message queue.
 *
 * The Controller class is designed to process SDL joystick events and convert
 * those into relevant messages. It also maintains a message queue to store and
 * retrieve these messages.
 */
class Controller {
public:

    /**
     * @brief Default constructor.
     *
     * Initializes SDL subsystems and sets up the joystick for input.
     */
    Controller();

        /**
     * @brief Destructor.
     *
     * Closes the SDL joystick and cleans up the SDL subsystems.
     */
    ~Controller();

    /**
     * @brief Reads the front message from the queue.
     *
     * Retrieves the next message from the queue and returns it.
     *
     * @return ControllerMessage The next message in the queue.
     */
    ControllerMessage readMessage();

        /**
     * @brief Processes SDL joystick events.
     *
     * Checks for pending SDL joystick events and processes them accordingly,
     * generating messages or handling system logic as needed.
     */
    void processEvents();

        /**
     * @brief Initializes SDL joystick subsystem.
     *
     * Sets up SDL for joystick input and opens the 
     * available joystick which is registered with MAC Address in Config.
     */
    void initializeSDL();


    /**
     * @brief Generates a payload based on a button press.
     *
     * Translates a button press into a relevant message payload.
     *
     * @param button The button number.
     * @return uint8_t The generated payload.
     */
    uint8_t generatePayload(uint8_t button);

        /**
     * @brief Generates a health check message.
     *
     * Constructs a message indicating the health or status of the controller.
     *
     * @return uint8_t The generated health check payload.
     */
    uint8_t generateHealthCheckMessage();
    std::queue<ControllerMessage> getMessageQueue();
    static uint8_t generateInitMessage();

private:
    SDL_Joystick* joystick_;    ///< SDL joystick handler.
    std::queue<ControllerMessage> messages_;    ///< Message queue for joystick input.
};


#endif //INC_4X4_GEWINNT_CONTROLLER_H
