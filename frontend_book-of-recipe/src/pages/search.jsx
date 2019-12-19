import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Link } from 'react-router-dom';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';
import IconButton from '@material-ui/core/IconButton';
import image_p from '../img/pancakes.jpg';
import image_m from '../img/meet.jpg';

const tileData = [
  {
    img: image_p,
    title: 'Блинчики',
  },
  {
    img: image_m,
    title: 'Мясо',
  },
  {
    img: image_p,
    title: 'Блинчики',
  },
  {
    img: image_m,
    title: 'Мясо',
  },
  {
    img: image_p,
    title: 'Блинчики',
  },
  {
    img: image_m,
    title: 'Мясо',
  },
];

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    backgroundColor: theme.palette.background.paper,
  },
  gridList: {
    width: 950,
    height: 500,
  },
  icon: {
    color: 'rgba(255, 255, 255, 0.54)',
  },
}));

export default function TitlebarGridList() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <GridList cols={3} cellHeight={200} spacing={50} className={classes.gridList}>
        {tileData.map(tile => (
          <GridListTile key={tile.img}>
            <img src={tile.img} alt={tile.title} />
            <Link to="/recipe">
              <GridListTileBar
                title={tile.title}
                actionIcon={
                  <Link to="/search">
                    <IconButton color={"secondary"} >&#10084;</IconButton>
                  </Link>
                }
              />
            </Link>
          </GridListTile>
        ))}
      </GridList>
    </div>
  );
}



/**

        <GridListTile key="Subheader" cols={4} style={{ height: 'auto' }}>
          <ListSubheader component="div">Результаты поиска</ListSubheader>
        </GridListTile>

*/