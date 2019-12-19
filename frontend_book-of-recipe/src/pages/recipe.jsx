import React, { Component } from 'react';
import { Container } from 'react-bootstrap';
import RecipeFull from '../components/recipefull'
export default class Recipe extends Component {
  state = {}
  render() {
    return (
      <Container>
        <RecipeFull />
      </Container>
    );
  }
}