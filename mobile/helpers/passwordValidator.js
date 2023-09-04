export function passwordValidator(password) {
  if (!password) return "Por favor, preencha este campo."
  if (password.length < 8) return 'A palavra-passe deve conter pelo menos 8 caracteres.'
  return ''
}
