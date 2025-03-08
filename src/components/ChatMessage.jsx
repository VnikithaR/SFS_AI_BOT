import React from 'react';
import ReactMarkdown from 'react-markdown';
import { motion } from 'framer-motion';

const ChatMessage = ({ message, isLast }) => {
  const isBot = message.type === 'bot';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`chat-message ${isBot ? 'bot-message' : 'user-message'}`}
    >
      {isBot && (
        <div className="flex items-center gap-2 mb-2">
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
            <span className="text-white text-sm">SFS</span>
          </div>
          <span className="font-medium text-sm">SFS Assistant</span>
        </div>
      )}
      <div className="message-content">
        <ReactMarkdown>{message.content}</ReactMarkdown>
      </div>
      <div className="text-xs opacity-70 mt-1">
        {new Date(message.timestamp).toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit'
        })}
      </div>
    </motion.div>
  );
};

export default ChatMessage;