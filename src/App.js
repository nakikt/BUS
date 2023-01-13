import { useEffect, useState } from 'react';
import './App.scss';
import Login from './Views/Login/Login';

import Dashboard from './Views/Dashboard/Dashboard';

function App() {

  const [user, setUser] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLogging, setIsLogging] = useState(false);

  // useEffect(() => {
  //   if(localStorage.getItem('user')) {
  //     setIsLoggedIn(true);
  //   }
  // }, [])

  return (
    <div className="App">
      {isLogging ? (
        <Login 
          user={user} setUser={setUser}
          isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn}
          setIsLogging={setIsLogging}
        />
      ) : (
        <Dashboard 
          user={user} setUser={setUser}
          isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn}
          setIsLogging={setIsLogging}
        />
      )}
          
    </div>
  );
}

export default App;
