import React from 'react';
import { Container } from 'react-bootstrap';
import Header from "./components/header"
import './App.css';
import Navbar from './components/navbar';
import SearchForm from './components/searchform';
import PopularMainItem from './components/popularmainitem'
function App() {
  return (
    <>
      <Header />
      <Container>
        <Navbar />
        <SearchForm />
        <PopularMainItem />
      </Container>
      <link
        rel="stylesheet"
        href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T"
        crossOrigin="anonymous"
      />
    </>
  );
}

export default App;
