import React from 'react';
import { motion } from 'framer-motion';

const QuickActions = ({ onActionClick }) => {
  const actions = [
    { id: 1, text: "Courses Offered", icon: "🎓" },
    { id: 2, text: "Admission Process", icon: "📝" },
    { id: 3, text: "Fee Structure", icon: "💰" },
    { id: 4, text: "Campus Facilities", icon: "🏛️" },
    { id: 5, text: "Contact Info", icon: "📞" },
    { id: 6, text: "Important Dates", icon: "📅" }
  ];

  return (
    <div className="bg-gray-50 p-2 flex gap-2 overflow-x-auto">
      {actions.map((action, index) => (
        <motion.button
          key={action.id}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.1 }}
          onClick={() => onActionClick(action.text)}
          className="quick-action-btn whitespace-nowrap flex items-center gap-2"
        >
          <span>{action.icon}</span>
          <span>{action.text}</span>
        </motion.button>
      ))}
    </div>
  );
};

export default QuickActions;