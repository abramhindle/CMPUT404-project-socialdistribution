import { Model, ModelStatic, Sequelize } from 'sequelize';
import { readdirSync } from 'fs';
import path from 'path';

if (
  !process.env.POSTGRES_USER &&
  !process.env.POSTGRES_PASSWORD &&
  !process.env.POSTGRES_HOST &&
  !process.env.POSTGRES_PORT &&
  !process.env.POSTGRES_DB
) {
  throw new Error('Database environment variables are not set');
}

const sequelize = new Sequelize(
  process.env.POSTGRES_DB,
  process.env.POSTGRES_USER,
  process.env.POSTGRES_PASSWORD,
  {
    host: process.env.POSTGRES_HOST,
    dialect: 'postgres',
    ...(process.env.NODE_ENV === 'test' && { logging: false }),
  }
);

readdirSync(__dirname + '/models')
  .filter((file: string) => {
    return (
      file.indexOf('.') !== 0 &&
      file !== path.basename(__filename) &&
      file.slice(-3) === '.ts'
    );
  })
  .forEach(async (file: string) => {
    const model: ModelStatic<Model> = await import(
      path.join(__dirname, '/models', file)
    );
    sequelize.modelManager.addModel(model);
  });

export default sequelize;
