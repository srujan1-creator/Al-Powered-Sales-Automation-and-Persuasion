import { useState, useRef, useEffect, memo } from 'react';
import PropTypes from 'prop-types';
import { sendMessage } from '../api';

const ChatInterface = memo(function ChatInterface({ conversation, onUpdate }) {
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
    // Maintain focus on input after sending/typing
    if (!isTyping) {
      inputRef.current?.focus();
    }
  }, [conversation.messages, isTyping]);

  useEffect(() => {
    // Initial focus
    inputRef.current?.focus();
  }, []);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;

    const userMessage = input;
    setInput('');
    setIsTyping(true);

    // Optimistically add user message to UI
    const optimisticConversation = {
      ...conversation,
      messages: [
        ...conversation.messages,
        { id: Date.now(), sender: 'user', content: userMessage }
      ]
    };
    onUpdate(optimisticConversation);

    try {
      const updatedConversation = await sendMessage(conversation.id, userMessage);
      onUpdate(updatedConversation);
    } catch (err) {
      console.error('Failed to send message:', err);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="chat-container" role="main" aria-label="Chat Interface">
      <div className="chat-header">
        <div className="avatar" aria-hidden="true">A</div>
        <div className="chat-header-info">
          <h2>Aura AI</h2>
          <p>Enterprise Sales Representative</p>
        </div>
      </div>
      
      <div className="chat-messages" role="log" aria-live="polite" aria-atomic="false">
        {conversation.messages.map((msg, idx) => (
          <div key={msg.id || idx} className={`message ${msg.sender}`} aria-label={`${msg.sender === 'user' ? 'You' : 'Aura'} said`}>
            {msg.content}
          </div>
        ))}
        {isTyping && (
          <div className="typing-indicator" aria-label="Aura is typing...">
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form className="chat-input-area" onSubmit={handleSend}>
        <input 
          id="chat-message-input"
          ref={inputRef}
          type="text" 
          placeholder="Type your message here..." 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isTyping}
          aria-label="Message input"
          aria-required="true"
          autoComplete="off"
        />
        <button type="submit" id="chat-send-btn" className="btn" disabled={!input.trim() || isTyping} aria-label="Send message">
          Send
        </button>
      </form>
    </div>
  );
});

ChatInterface.propTypes = {
  conversation: PropTypes.shape({
    id: PropTypes.number.isRequired,
    messages: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number,
        sender: PropTypes.string.isRequired,
        content: PropTypes.string.isRequired,
      })
    ).isRequired,
  }).isRequired,
  onUpdate: PropTypes.func.isRequired,
};

export default ChatInterface;
