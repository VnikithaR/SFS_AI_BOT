export const collegeData = {
  courses: {
    undergraduate: [
      {
        name: "BCom",
        variants: ["Regular", "Professional", "Honors"],
        duration: "3 years",
        details: "Bachelor of Commerce program offering comprehensive business education"
      },
      {
        name: "BBA",
        duration: "3 years",
        details: "Bachelor of Business Administration focusing on management principles"
      },
      {
        name: "BCA",
        duration: "3 years",
        details: "Bachelor of Computer Applications with focus on software development"
      },
      {
        name: "BSc",
        variants: ["Computer Science", "Mathematics", "Electronics"],
        duration: "3 years",
        details: "Bachelor of Science programs in various disciplines"
      }
    ],
    postgraduate: [
      {
        name: "MBA",
        duration: "2 years",
        details: "Master of Business Administration with various specializations"
      },
      {
        name: "MCom",
        duration: "2 years",
        details: "Master of Commerce with advanced business studies"
      },
      {
        name: "MA",
        duration: "2 years",
        details: "Master of Arts programs"
      }
    ]
  },
  admissions: {
    process: [
      "Online application submission",
      "Document verification",
      "Entrance test (for specific courses)",
      "Interview process",
      "Merit-based selection",
      "Fee payment and enrollment"
    ],
    requirements: {
      undergraduate: "Minimum 60% in 10+2 or equivalent",
      postgraduate: "Minimum 55% in relevant bachelor's degree"
    },
    documents: [
      "10th and 12th mark sheets",
      "Transfer certificate",
      "Character certificate",
      "Passport size photographs",
      "Identity proof",
      "Address proof"
    ]
  },
  facilities: {
    academic: [
      "Modern classrooms",
      "Digital library",
      "Computer labs",
      "Science laboratories",
      "Seminar halls"
    ],
    sports: [
      "Indoor sports complex",
      "Outdoor sports grounds",
      "Gymnasium",
      "Athletics track"
    ],
    others: [
      "Wi-Fi campus",
      "Cafeteria",
      "Medical facility",
      "Transport facility",
      "Hostel accommodation"
    ]
  },
  contact: {
    address: "23, Hosur Road, Bangalore - 560029, Karnataka, India",
    phone: ["+91-80-22245566", "+91-80-22245567"],
    email: "info@sfscollege.in",
    website: "www.sfscollege.in"
  },
  importantDates: {
    admissions: {
      start: "January 2025",
      end: "July 2025"
    },
    examSchedule: {
      midterm: "March 2025",
      endterm: "May 2025"
    },
    events: [
      {
        name: "College Day",
        date: "March 15, 2025"
      },
      {
        name: "Sports Meet",
        date: "February 2025"
      }
    ]
  }
};

export const generateResponse = (query) => {
  const lowerQuery = query.toLowerCase();
  
  // Course related queries
  if (lowerQuery.includes('course') || lowerQuery.includes('program')) {
    if (lowerQuery.includes('bcom') || lowerQuery.includes('commerce')) {
      return {
        type: 'courses',
        content: "The BCom program at SFS College offers three variants:\n\n" +
                "1. BCom Regular\n2. BCom Professional\n3. BCom Honors\n\n" +
                "Key features:\n" +
                "- 3-year duration\n" +
                "- Industry-aligned curriculum\n" +
                "- Experienced faculty\n" +
                "- Regular industry interactions\n\n" +
                "Would you like to know more about admission requirements?"
      };
    }
    return {
      type: 'courses',
      content: "SFS College offers various undergraduate and postgraduate programs:\n\n" +
               "**Undergraduate Programs:**\n" +
               "- BCom (Regular, Professional, Honors)\n" +
               "- BBA (Bachelor of Business Administration)\n" +
               "- BCA (Bachelor of Computer Applications)\n" +
               "- BSc (Computer Science, Mathematics, Electronics)\n\n" +
               "**Postgraduate Programs:**\n" +
               "- MBA\n" +
               "- MCom\n" +
               "- MA\n\n" +
               "Which program would you like to know more about?"
    };
  }

  // Admission related queries
  if (lowerQuery.includes('admission') || lowerQuery.includes('apply')) {
    return {
      type: 'admissions',
      content: "**Admission Process at SFS College:**\n\n" +
               "1. Online Application\n" +
               "2. Document Verification\n" +
               "3. Entrance Test (for specific courses)\n" +
               "4. Interview\n" +
               "5. Merit-based Selection\n\n" +
               "**Required Documents:**\n" +
               "- 10th and 12th mark sheets\n" +
               "- Transfer certificate\n" +
               "- Character certificate\n" +
               "- Photographs\n" +
               "- ID proof\n\n" +
               "Would you like to know about eligibility criteria or fee structure?"
    };
  }

  // Facilities related queries
  if (lowerQuery.includes('facility') || lowerQuery.includes('infrastructure')) {
    return {
      type: 'facilities',
      content: "SFS College offers world-class facilities:\n\n" +
               "**Academic Facilities:**\n" +
               "- Modern classrooms with projectors\n" +
               "- Digital library\n" +
               "- Computer labs\n" +
               "- Science laboratories\n" +
               "- Seminar halls\n\n" +
               "**Sports Facilities:**\n" +
               "- Indoor sports complex\n" +
               "- Outdoor sports grounds\n" +
               "- Gymnasium\n" +
               "- Athletics track\n\n" +
               "**Other Facilities:**\n" +
               "- Wi-Fi enabled campus\n" +
               "- Cafeteria\n" +
               "- Medical facility\n" +
               "- Transport\n" +
               "- Hostel accommodation"
    };
  }

  // Contact related queries
  if (lowerQuery.includes('contact') || lowerQuery.includes('address') || lowerQuery.includes('phone')) {
    return {
      type: 'contact',
      content: "**Contact Information:**\n\n" +
               "**Address:**\n" +
               "23, Hosur Road\n" +
               "Bangalore - 560029\n" +
               "Karnataka, India\n\n" +
               "**Phone:**\n" +
               "+91-80-22245566\n" +
               "+91-80-22245567\n\n" +
               "**Email:** info@sfscollege.in\n" +
               "**Website:** www.sfscollege.in"
    };
  }

  // Default response
  return {
    type: 'general',
    content: "I understand you're asking about " + query + ". Could you please be more specific? I can help you with:\n\n" +
             "- Course information\n" +
             "- Admission process\n" +
             "- College facilities\n" +
             "- Contact details\n" +
             "- Important dates"
  };
};