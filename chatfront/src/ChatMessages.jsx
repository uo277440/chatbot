function ChatMessages({ messages }) {
    return (
        <div className="chat-messages">
            {messages.map((message, index) => (
                <div key={index} className={`message ${message.from}`}>
                    {message.text}
                </div>
            ))}
        </div>
    );
}
export default ChatMessages;