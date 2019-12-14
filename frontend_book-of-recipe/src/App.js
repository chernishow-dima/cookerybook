import React from 'react';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { Container } from 'react-bootstrap';
import Start from './pages/start';

import Search from './pages/search';
import Header from './components/header';
import Navbar from './components/navbar';
import SearchForm from './components/searchform';
export default function App() {
  return (
    <Router>
      <Header />
      <Container>
        <Navbar />
        <SearchForm />
      </Container>
      <Switch>
        <Route path='/search' component={Search}></Route>
        <Route path='/' component={Start}></Route>
      </Switch>
    </Router>
  );
}
