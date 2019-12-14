import React, { Component } from 'react';
import { Container } from 'react-bootstrap';
import Header from "../components/header"
import '../App.css';
import Navbar from '../components/navbar';
import SearchForm from '../components/searchform';
import PopularMainItem from '../components/popularmainitem'

export default class Start extends Component {
  render() {
    return (
      <>
        <Container>
          <PopularMainItem />
        </Container>
      </>
    )
  };

}