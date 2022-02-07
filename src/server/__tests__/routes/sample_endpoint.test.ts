import request from 'supertest';
import app from '../../src/app';

describe('Sample Endpoints', () => {
  it('should do something', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toEqual(404);
  });
});
