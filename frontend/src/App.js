import React from 'react';
import './App.css';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import {Home, About, Reports, Translator, NoMatch} from './pages/index';
import {Layout, NavigationBar} from  './components/index';

function App() {
  return (
    <>
      <NavigationBar/>
      <Layout>
        <Router>
          <Switch>
            <Route exact path="/" component={Home}/>
            <Route path="/about" component={About}/>
            <Route path="/reports" component={Reports}/>
            <Route path="/translator" component={Translator}/>
            <Route component={NoMatch}/>
          </Switch>
        </Router>
      </Layout>
    </>
  );
}

export default App;
