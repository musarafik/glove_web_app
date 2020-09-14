import React from 'react';
import './App.css';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import {Home, About, Reports, Translator, NoMatch, Learn, Test, AdditionalResources} from './pages/index';
import {Layout, NavigationBar} from  './components/index';

function App() {
  return (
    <div style={{backgroundColor:'#DBF1FF', backgroundSize:'cover', backgroundRepeat: 'repeat', height:'100vh'}}>
      <NavigationBar/>
      <Layout>
        <Router>
          <Switch>
            <Route exact path="/" component={Home}/>
            <Route path="/about" component={About}/>
            <Route path="/reports" component={Reports}/>
            <Route path="/translator" component={Translator}/>
            <Route path="/learn" component={Learn}/>
            <Route path="/test" component={Test}/>
            <Route path="/additionalResources" component={AdditionalResources}/>
            <Route component={NoMatch}/>
          </Switch>
        </Router>
      </Layout>
    </div>
  );
}

export default App;
