module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'refactor', 'chore', 'docs', 'test'],
    ],
    'scope-enum': [
      2,
      'always',
      [
        'models',
        'enums',
        'services',
        'repositories',
        'routes',
        'schemas',
        'auth',
        'frontend',
        'backend',
        'ci',
        'docs',
      ],
    ],
    'subject-case': [2, 'always', 'sentence-case'],
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 72],
  },
};
