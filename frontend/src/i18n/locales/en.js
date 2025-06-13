export default {
  general: {
    submit: 'Confirm',
    create: 'Create',
    delete: 'Delete',
    cancel: 'Cancel',

    pageNotFound: 'Page is not found',

    copyLink: 'Copy link',
    linkCopied: 'Link has been copied',
    downloadTable: 'Download table',

    min: 'min. {n}',
    max: 'max. {n}',
    fromAToB: 'from {a} to {b}',

    maxChar: '@:general.max char.',

    overview: 'Overview',
    at: 'at',
    view: 'View',

    irreversible: 'This action is irreversible',
  },
  profile: {
    profile: 'Profile',
  },
  
  forms: {
    form: 'Form',
    forms: 'Forms',
    question: 'Question',
    submission: 'Submission',
    answers: 'Answers',
    questionsNumber: 'no questions | {n} question | {n} questions',
    submissionsNumber: '{n} submissions | {n} submission | {n} submissions',
    answersNumber: 'no answers | {n} answer | {n} answers',

    active: 'Active',
    closed: 'Closed',

    close: 'Close',
    closeForm: 'Close form',
    closeFormConfirm: 'Are you sure you want to close this form? New submissions will be impossible.',

    closedMessage: 'This form is closed. New submissions are impossible.',

    title: 'Title',
    description: 'Description',
    required: 'required',
    notRequired: 'not required',
    selectQuestionType: 'Select question type',

    types: {
      text: 'Text',
      number: 'Number',
      color: 'Color',
      choice: 'Choice'
    },

    choices: {
      variant: 'Variant',
      addVariant: 'Add variant',
    },

    restrictionsLabel: 'Restrictions',

    addQuestion: 'Add question',
    delete: 'Delete Form',

    confirmDelete: 'Are you sure you want to delete this form? You will lose all submissions. Maybe you want to close it instead?',

    formSuccessfullyCreated: 'Form has been successfully created!',
    nowYouCanShareViaLink: 'Now you can share it using link',

    formSuccessfullySubmitted: 'Form has been successfully submitted!',

    restrictions: {
      maxAnswerLength: 'Max answer length',
      maxValue: 'Max value',
      minValue: 'Min value',
      numericAnswerType: 'Answer type',
      canBeFloat: 'Can be float number',
      regex: 'Regular expression',
    },

    byQuestions: 'By questions',
    bySubmissions: 'By submissions',

    noAnswer: 'no answer',

    averageValue: 'Average value',
  },
  placeholders: {
    number: 'number',
    regex: '\\d{3}'
  },
  auth: {
    login: 'Login',
    loginButton: '@:auth.login',
    register: 'Register',
    registerButton: '@:auth.register',
    username: 'username',
    password: 'password',
    confirmPassword: 'confirm password',
    logout: 'Logout',

    enterPassword: 'Enter password',
    weakPassword: 'Too weak',
    mediumPassword: 'Medium',
    strongPassword: 'Great!',
  },
  landing: {
    title: {
      creating: 'Creating',
      forms: 'Forms',
      hasNeverBeenThatEasy: 'has never been that easy!',
    },
    features: {
      features: 'Features',
      first: {
        title: 'Easily restrict answers',
        text: 'Restrict your text answers with regular expressions and define max length. For number answers you can set min and max values',
      },
      second: {
        title: 'Get notifications on new submissions',
        text: 'Connect our Telegram bot and get notifications everytime someone answers your form',
      },
      third: {
        title: 'Export all answers in Excel table',
        text: 'You can easily export all answers on your form in an universal format',
      },
    }
  },
}