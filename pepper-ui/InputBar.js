const sendMessage = async (text) => {
    const newMsg = { sender: "user", text };
    setMessages(prev => [...prev, newMsg]);
  
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
  
    const data = await res.json();
  
    setMessages(prev => [
      ...prev,
      { sender: "bot", text: data.response }
    ]);
  };