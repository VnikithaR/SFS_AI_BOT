import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, Send, RefreshCcw, Info, X, Minimize2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import ChatMessage from './components/ChatMessage';
import QuickActions from './components/QuickActions';
import { generateResponse } from './data/collegeData';

const initialMessage = {
  type: 'bot',
  content: "Hello! I'm SFS Assistant, your AI guide to St. Francis de Sales College. How can I help you today?",
  timestamp: new Date()
};

function App() {
  const [messages, setMessages] = useState([initialMessage]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showInfo, setShowInfo] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [showFeedback, setShowFeedback] = useState(false);
  const chatContainerRef = useRef(null);

  const categories = [
    { title: "Courses and Programs", icon: "🎓" },
    { title: "Admissions and Deadlines", icon: "📅" },
    { title: "Campus Facilities", icon: "🏛️" },
    { title: "Contact Information", icon: "📞" },
    { title: "Faculty Details", icon: "👨‍🏫" },
    { title: "Hostel Accommodation", icon: "🏠" },
  ];

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      type: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      const response = generateResponse(input);
      setTimeout(() => {
        const botResponse = {
          type: 'bot',
          content: response.content,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, botResponse]);
        setIsTyping(false);
        setShowFeedback(true);
      }, 1000);
    } catch (error) {
      const errorMessage = {
        type: 'bot',
        content: "I apologize, but I'm having trouble processing your request. Please try again.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
      setIsTyping(false);
    }
  };

  const handleQuickAction = (action) => {
    setInput(action);
    handleSend();
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const resetChat = () => {
    setMessages([initialMessage]);
    setInput('');
    setShowFeedback(false);
  };

  const toggleMinimize = () => {
    setIsMinimized(!isMinimized);
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <AnimatePresence>
        {!isMinimized ? (
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 50 }}
            className="max-w-[400px] w-full shadow-xl rounded-lg overflow-hidden bg-white"
          >
            {/* Header */}
            <div className="bg-primary p-4 flex justify-between items-center">
              <div className="flex items-center gap-2 text-white">
                <MessageCircle size={24} />
                <h1 className="font-semibold">SFS College Assistant</h1>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={resetChat}
                  className="p-2 hover:bg-blue-700 rounded-full transition-colors"
                >
                  <RefreshCcw size={20} className="text-white" />
                </button>
                <button
                  onClick={() => setShowInfo(!showInfo)}
                  className="p-2 hover:bg-blue-700 rounded-full transition-colors"
                >
                  <Info size={20} className="text-white" />
                </button>
                <button
                  onClick={toggleMinimize}
                  className="p-2 hover:bg-blue-700 rounded-full transition-colors"
                >
                  <Minimize2 size={20} className="text-white" />
                </button>
              </div>
            </div>

            {/* Info Panel */}
            <AnimatePresence>
              {showInfo && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="bg-white p-4 border-b"
                >
                  <h2 className="font-semibold mb-2">I can help you with:</h2>
                  <div className="grid grid-cols-2 gap-2">
                    {categories.map((category, index) => (
                      <div key={index} className="flex items-center gap-2 text-sm">
                        <span>{category.icon}</span>
                        <span>{category.title}</span>
                      </div>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Chat Container */}
            <div
              ref={chatContainerRef}
              className="bg-gray-50 p-4 chat-container"
              style={{ height: '400px' }}
            >
              {messages.map((message, index) => (
                <ChatMessage
                  key={index}
                  message={message}
                  isLast={index === messages.length - 1}
                />
              ))}
              {isTyping && (
                <div className="typing-indicator">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <QuickActions onActionClick={handleQuickAction} />

            {/* Input Area */}
            <div className="bg-white p-4 flex gap-2 items-center border-t">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about SFS College..."
                className="flex-1 p-2 border rounded-lg focus:outline-none focus:border-primary"
              />
              <button
                onClick={handleSend}
                disabled={!input.trim()}
                className="p-2 bg-primary text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                <Send size={20} />
              </button>
            </div>

            {/* Footer */}
            <div className="bg-gray-50 p-2 text-center text-xs text-gray-500">
              SFS College Assistant - AI-powered support
            </div>
          </motion.div>
        ) : (
          <motion.button
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0 }}
            onClick={toggleMinimize}
            className="bg-primary text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition-colors"
          >
            <MessageCircle size={24} />
          </motion.button>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;