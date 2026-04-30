import { useState, useCallback } from 'react';
import Onboarding from './components/Onboarding';
import ChatInterface from './components/ChatInterface';
import Dashboard from './components/Dashboard';

function App() {
  const [conversation, setConversation] = useState(null);
  const [context, setContext] = useState(null);

  const handleContextCreated = useCallback((newConversation, initialContext) => {
    setConversation(newConversation);
    setContext(initialContext);
  }, []);

  const handleConversationUpdate = useCallback((updatedConversation) => {
    setConversation(updatedConversation);
  }, []);

  return (
    <>
      {!conversation ? (
        <Onboarding onComplete={handleContextCreated} />
      ) : (
        <div className="app-container animate-fade-in">
          <main className="main-content glass-panel">
            <ChatInterface 
              conversation={conversation} 
              onUpdate={handleConversationUpdate} 
            />
          </main>
          <aside className="sidebar">
            <Dashboard 
              conversation={conversation} 
              context={context} 
            />
          </aside>
        </div>
      )}
    </>
  );
}

export default App;
