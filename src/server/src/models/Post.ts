import { DataTypes, Model } from 'sequelize';
import db from '../db';
import { v4 as uuidv4 } from 'uuid';

class Post extends Model {
  declare id: typeof uuidv4;
  declare title: string;
  declare source: string;
  declare origin: string;
  declare description: string;
  declare contentType:
    | 'text/markdown'
    | 'text/plain'
    | 'application/base64'
    | 'image/png;base64'
    | 'image/jpeg;base64';
  declare content: string;
  declare image: string;
  declare categories: string[];
  declare count: number;
  declare published: Date;
  declare visibility: 'PUBLIC' | 'FRIENDS';
  declare unlisted: boolean;
}

Post.init(
  {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      allowNull: false,
      primaryKey: true,
    },
    title: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    source: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    origin: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    description: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    contentType: {
      type: DataTypes.STRING,
      allowNull: false,
      defaultValue: 'text/plain',
      validate: {
        customValidator: value => {
          const enums = [
            'text/markdown',
            'text/plain',
            'application/base64',
            'image/png;base64',
            'image/jpeg;base64',
          ];
          if (!enums.includes(value)) {
            throw new Error('Not a valid option');
          }
        },
      },
    },
    content: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    image: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    categories: {
      type: DataTypes.ARRAY(DataTypes.STRING),
      allowNull: false,
    },
    count: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 0,
    },
    published: {
      type: DataTypes.DATE,
      allowNull: false,
      defaultValue: DataTypes.NOW,
    },
    visibility: {
      type: DataTypes.STRING,
      allowNull: false,
      defaultValue: 'PUBLIC',
      validate: {
        customValidator: value => {
          const enums = ['PUBLIC', 'FRIENDS'];
          if (!enums.includes(value)) {
            throw new Error('Not a valid option');
          }
        },
      },
    },
    unlisted: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: false,
    },
  },
  {
    sequelize: db,
    modelName: 'Post',
    underscored: true,
  }
);

export default Post;
