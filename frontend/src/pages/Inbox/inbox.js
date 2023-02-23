import logo from '../../logo.svg';
import './inbox.css';

function Inbox() {
  return (
    <div className="Inbox">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          This is now the inbox page
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default Inbox;