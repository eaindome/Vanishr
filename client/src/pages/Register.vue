<template>
  <div class="signup-container">
    <div class="signup-card">
      <!-- Logo Section -->
      <div class="logo-section">
        <div class="logo-placeholder">
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
            <rect width="48" height="48" rx="12" fill="#4F46E5"/>
            <path d="M24 16L32 24L24 32L16 24L24 16Z" fill="white"/>
          </svg>
        </div>
        <h1 class="app-title">Create Account</h1>
        <p class="app-subtitle">Join us to protect your digital privacy</p>
      </div>

      <!-- Form Section -->
      <form @submit.prevent="handleSignup" class="signup-form">
        <div class="form-row">
          <div class="form-group">
            <label for="firstName" class="form-label">First Name</label>
            <input
              id="firstName"
              v-model="form.firstName"
              type="text"
              class="form-input"
              :class="{ 'form-input-error': errors.firstName }"
              placeholder="John"
              required
            />
            <span v-if="errors.firstName" class="error-message">{{ errors.firstName }}</span>
          </div>

          <div class="form-group">
            <label for="lastName" class="form-label">Last Name</label>
            <input
              id="lastName"
              v-model="form.lastName"
              type="text"
              class="form-input"
              :class="{ 'form-input-error': errors.lastName }"
              placeholder="Doe"
              required
            />
            <span v-if="errors.lastName" class="error-message">{{ errors.lastName }}</span>
          </div>
        </div>

        <div class="form-group">
          <label for="email" class="form-label">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="form-input"
            :class="{ 'form-input-error': errors.email }"
            placeholder="john.doe@example.com"
            required
          />
          <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
        </div>

        <div class="form-group">
          <label for="password" class="form-label">Password</label>
          <div class="password-input-container">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              class="form-input password-input"
              :class="{ 'form-input-error': errors.password }"
              placeholder="Create a strong password"
              required
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="password-toggle"
            >
              <svg v-if="!showPassword" width="20" height="20" fill="currentColor">
                <path d="M10 3C6.5 3 3.5 5.5 2 10c1.5 4.5 4.5 7 8 7s6.5-2.5 8-7c-1.5-4.5-4.5-7-8-7zm0 11.5c-2.5 0-4.5-2-4.5-4.5S7.5 5.5 10 5.5s4.5 2 4.5 4.5-2 4.5-4.5 4.5z"/>
                <circle cx="10" cy="10" r="2"/>
              </svg>
              <svg v-else width="20" height="20" fill="currentColor">
                <path d="M2 10s3-7 8-7 8 7 8 7-3 7-8 7-8-7-8-7z"/>
                <path d="M10 13a3 3 0 100-6 3 3 0 000 6z"/>
                <path d="M2 2l16 16"/>
              </svg>
            </button>
          </div>
          <div class="password-strength" v-if="form.password">
            <div class="strength-bar">
              <div
                class="strength-fill"
                :class="passwordStrengthClass"
                :style="{ width: passwordStrengthWidth }"
              ></div>
            </div>
            <span class="strength-text" :class="passwordStrengthClass">
              {{ passwordStrengthText }}
            </span>
          </div>
          <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
        </div>

        <div class="form-group">
          <label for="confirmPassword" class="form-label">Confirm Password</label>
          <div class="password-input-container">
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              class="form-input password-input"
              :class="{ 'form-input-error': errors.confirmPassword }"
              placeholder="Confirm your password"
              required
            />
            <button
              type="button"
              @click="showConfirmPassword = !showConfirmPassword"
              class="password-toggle"
            >
              <svg v-if="!showConfirmPassword" width="20" height="20" fill="currentColor">
                <path d="M10 3C6.5 3 3.5 5.5 2 10c1.5 4.5 4.5 7 8 7s6.5-2.5 8-7c-1.5-4.5-4.5-7-8-7zm0 11.5c-2.5 0-4.5-2-4.5-4.5S7.5 5.5 10 5.5s4.5 2 4.5 4.5-2 4.5-4.5 4.5z"/>
                <circle cx="10" cy="10" r="2"/>
              </svg>
              <svg v-else width="20" height="20" fill="currentColor">
                <path d="M2 10s3-7 8-7 8 7 8 7-3 7-8 7-8-7-8-7z"/>
                <path d="M10 13a3 3 0 100-6 3 3 0 000 6z"/>
                <path d="M2 2l16 16"/>
              </svg>
            </button>
          </div>
          <span v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</span>
        </div>

        <!-- Terms and Privacy Checkbox -->
        <div class="form-group checkbox-group">
          <label class="checkbox-label">
            <input
              type="checkbox"
              v-model="form.agreedToTerms"
              class="checkbox-input"
              required
            />
            <span class="checkbox-custom"></span>
            <span class="checkbox-text">
              I agree to the <a href="#" class="terms-link">Terms of Service</a> and
              <a href="#" class="terms-link">Privacy Policy</a>
            </span>
          </label>
          <span v-if="errors.agreedToTerms" class="error-message">{{ errors.agreedToTerms }}</span>
        </div>

        <!-- Marketing Checkbox (Optional) -->
        <div class="form-group checkbox-group">
          <label class="checkbox-label">
            <input
              type="checkbox"
              v-model="form.marketingEmails"
              class="checkbox-input"
            />
            <span class="checkbox-custom"></span>
            <span class="checkbox-text">
              Send me product updates and privacy tips (optional)
            </span>
          </label>
        </div>

        <button type="submit" class="signup-button" :disabled="isLoading">
          <span v-if="!isLoading">Create Account</span>
          <div v-else class="loading-spinner"></div>
        </button>
      </form>

      <!-- Divider -->
      <div class="divider">
        <span>or</span>
      </div>

      <!-- Social Login -->
      <div class="social-section">
        <button type="button" class="social-button google-button">
          <svg width="20" height="20" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          Sign up with Google
        </button>
      </div>

      <!-- Login Link -->
      <div class="login-section">
        <p class="login-text">
          Already have an account?
          <router-link to="/login" class="login-link">Sign in</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreedToTerms: false,
  marketingEmails: false
})

const errors = reactive<{
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirmPassword: string;
  agreedToTerms: string;
  [key: string]: string;
}>({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreedToTerms: ''
})

const isLoading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const passwordStrength = computed(() => {
  const password = form.password
  if (!password) return 0

  let strength = 0
  if (password.length >= 8) strength += 25
  if (/[a-z]/.test(password)) strength += 25
  if (/[A-Z]/.test(password)) strength += 25
  if (/[0-9]/.test(password)) strength += 12.5
  if (/[^A-Za-z0-9]/.test(password)) strength += 12.5

  return Math.min(strength, 100)
})

const passwordStrengthClass = computed(() => {
  const strength = passwordStrength.value
  if (strength < 25) return 'strength-weak'
  if (strength < 50) return 'strength-fair'
  if (strength < 75) return 'strength-good'
  return 'strength-strong'
})

const passwordStrengthWidth = computed(() => `${passwordStrength.value}%`)

const passwordStrengthText = computed(() => {
  const strength = passwordStrength.value
  if (strength < 25) return 'Weak'
  if (strength < 50) return 'Fair'
  if (strength < 75) return 'Good'
  return 'Strong'
})

const validateForm = () => {
  // Reset errors
  Object.keys(errors).forEach(key => errors[key] = '')

  let isValid = true

  if (!form.firstName.trim()) {
    errors.firstName = 'First name is required'
    isValid = false
  }

  if (!form.lastName.trim()) {
    errors.lastName = 'Last name is required'
    isValid = false
  }

  if (!form.email) {
    errors.email = 'Email is required'
    isValid = false
  } else if (!/\S+@\S+\.\S+/.test(form.email)) {
    errors.email = 'Please enter a valid email'
    isValid = false
  }

  if (!form.password) {
    errors.password = 'Password is required'
    isValid = false
  } else if (form.password.length < 8) {
    errors.password = 'Password must be at least 8 characters'
    isValid = false
  }

  if (!form.confirmPassword) {
    errors.confirmPassword = 'Please confirm your password'
    isValid = false
  } else if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
    isValid = false
  }

  if (!form.agreedToTerms) {
    errors.agreedToTerms = 'You must agree to the terms to continue'
    isValid = false
  }

  return isValid
}

const handleSignup = async () => {
  if (!validateForm()) return

  isLoading.value = true

  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))

    // Replace with actual API call to your FastAPI backend
    // const response = await api.signup({
    //   first_name: form.firstName,
    //   last_name: form.lastName,
    //   email: form.email,
    //   password: form.password,
    //   marketing_emails: form.marketingEmails
    // })

    // On success, redirect to login or dashboard
    router.push('/login?message=Account created successfully')
  } catch (error) {
    console.error('Signup failed:', error)
    errors.email = 'An account with this email already exists'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.signup-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.signup-card {
  background: white;
  border-radius: 20px;
  padding: 3rem 2rem;
  width: 100%;
  max-width: 480px;
  box-shadow:
    0 0 0 1px rgba(0, 0, 0, 0.05),
    0 4px 24px rgba(0, 0, 0, 0.06),
    0 16px 48px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.logo-section {
  text-align: center;
  margin-bottom: 2.5rem;
}

.logo-placeholder {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.app-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.025em;
}

.app-subtitle {
  color: #64748b;
  font-size: 0.95rem;
  margin: 0;
  font-weight: 400;
}

.signup-form {
  margin-bottom: 2rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row .form-group {
  margin-bottom: 0;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
  letter-spacing: -0.01em;
}

.form-input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  color: #1e293b;
  background: #ffffff;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
  background: #ffffff;
}

.form-input::placeholder {
  color: #94a3b8;
}

.form-input-error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.password-input-container {
  position: relative;
}

.password-input {
  padding-right: 3rem;
}

.password-toggle {
  position: absolute;
  right: 0.875rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: color 0.2s ease;
}

.password-toggle:hover {
  color: #64748b;
}

.password-strength {
  margin-top: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.strength-bar {
  flex: 1;
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.strength-weak { background-color: #ef4444; color: #ef4444; }
.strength-fair { background-color: #f59e0b; color: #f59e0b; }
.strength-good { background-color: #10b981; color: #10b981; }
.strength-strong { background-color: #059669; color: #059669; }

.strength-text {
  font-size: 0.75rem;
  font-weight: 500;
  min-width: 50px;
}

.checkbox-group {
  margin-bottom: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  gap: 0.75rem;
}

.checkbox-input {
  display: none;
}

.checkbox-custom {
  width: 18px;
  height: 18px;
  border: 1.5px solid #d1d5db;
  border-radius: 4px;
  background: white;
  position: relative;
  flex-shrink: 0;
  margin-top: 2px;
  transition: all 0.2s ease;
}

.checkbox-input:checked + .checkbox-custom {
  background: #4f46e5;
  border-color: #4f46e5;
}

.checkbox-input:checked + .checkbox-custom::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 5px;
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-text {
  font-size: 0.875rem;
  color: #374151;
  line-height: 1.4;
}

.terms-link {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.terms-link:hover {
  color: #4338ca;
}

.error-message {
  display: block;
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  font-weight: 400;
}

.signup-button {
  width: 100%;
  background: #4f46e5;
  color: white;
  border: none;
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: -0.01em;
  margin-top: 1rem;
}

.signup-button:hover:not(:disabled) {
  background: #4338ca;
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(79, 70, 229, 0.2);
}

.signup-button:active {
  transform: translateY(0);
}

.signup-button:disabled {
  background: #94a3b8;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.divider {
  position: relative;
  text-align: center;
  margin: 2rem 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e2e8f0;
}

.divider span {
  background: white;
  padding: 0 1rem;
  color: #94a3b8;
  font-size: 0.875rem;
  font-weight: 400;
}

.social-section {
  margin-bottom: 2rem;
}

.social-button {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  background: white;
  color: #374151;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.social-button:hover {
  border-color: #d1d5db;
  background: #f9fafb;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.login-section {
  text-align: center;
}

.login-text {
  color: #64748b;
  font-size: 0.95rem;
  margin: 0;
}

.login-link {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.login-link:hover {
  color: #4338ca;
}

/* Responsive Design */
@media (max-width: 580px) {
  .signup-card {
    padding: 2rem 1.5rem;
    border-radius: 16px;
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .form-row .form-group {
    margin-bottom: 1.5rem;
  }

  .app-title {
    font-size: 1.5rem;
  }

  .form-input {
    padding: 0.75rem;
  }

  .signup-button {
    padding: 0.75rem 1.25rem;
  }
}

@media (max-width: 480px) {
  .signup-container {
    padding: 1rem;
  }
}
</style>
