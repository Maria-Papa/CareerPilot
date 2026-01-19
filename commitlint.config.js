module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Allowed commit types (aligned with APP_STYLE_MANIFEST)
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'refactor', 'chore', 'docs', 'test'],
    ],

    // Allowed scopes (architecture + domain + persistence)
    'scope-enum': [
      2,
      'always',
      [
        // architecture
        'backend',
        'frontend',
        'api',
        'infra',
        'style',
        'tooling',
        'ci',
        'adr',

        // domain
        'jobs',
        'interviews',
        'files',
        'auth',
        'users',
        'companies',

        // persistence
        'models',
        'enums',
        'db',
        'migrations',
      ],
    ],

    // Subject formatting rules
    'subject-case': [2, 'always', 'sentence-case'],
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 72],
  },
};
