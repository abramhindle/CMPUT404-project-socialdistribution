/** @type {import('ts-jest/dist/types').InitialOptionsTsJest} */
module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'jsdom',
    transform: {
        '^.+\\.ts?$': 'ts-jest',
        '^.+\\.(js|jsx)$': 'babel-jest',
    },
    testPathIgnorePatterns: ['src/pages/__tests__/Mainpage.test.tsx'],
    transformIgnorePatterns: ['/node_modules/(?!(react-markdown)/)'],
};