#ifndef SERIAL_HANDLER_H_
#define SERIAL_HANDLER_H_

class SerialHandler
{
    public:
    SerialHandler();
    SerialHandler(char *outbound_buf);

    public:
    void ReceiveSerial();
    bool IsSerialActive();
    bool IsDataReady();

    private:
    char inbound_buffer_[3];
    char *outbound_buffer_;
    char char_buf_;
    bool serial_active_;
    bool data_ready_;
    int inbound_cursor_;
    int outbound_cursor_;
};

SerialHandler::SerialHandler()
  : serial_active_(false), data_ready_(true),
    outbound_buffer_(NULL)
{
    memset(inbound_buffer_, '\0', 3);
}

SerialHandler::SerialHandler(char *outbound_buf)
  : serial_active_(false), data_ready_(true),
    outbound_buffer_(outbound_buf)
{
    memset(inbound_buffer_, '\0', 3);
}

void SerialHandler::ReceiveSerial()
{
    if (Serial.available())
    {
        if (!serial_active_)
        {
            serial_active_ = true;
            data_ready_ = false;
            inbound_cursor_ = -1;
        }

        char_buf_ = Serial.read();
        inbound_buffer_[++inbound_cursor_] = char_buf_;

        if (char_buf_ == '\n')
        {
            inbound_buffer_[inbound_cursor_] == '\0';
            serial_active_ = false;
            data_ready_ = true;
            inbound_cursor_ = -1;
        }
    }
}

bool SerialHandler::IsSerialActive()
{
    return serial_active_;
}

bool SerialHandler::IsDataReady()
{
    return data_ready_;
}

#endif
