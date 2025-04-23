<script setup>
import { useAuth } from "@/composables/useAuth";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const auth = useAuth();

const username = ref(localStorage.getItem('username') != 'undefined' ? localStorage.getItem('username') : "");
const password = ref("");
const errorMessage = ref("");
const loading = ref(false)

const login = async () => {
  const creds = { username: username.value, password: password.value };
  loading.value = true;
  try {
    await auth.login(creds);
    router.push('/profile');
  } catch (error) {
    if (error.response?.status === 400) {
      console.log(error.response.data);
    } else if (error.response?.status === 401) {
      errorMessage.value = "Invalid username or password"
      password.value = '';
    } else {
      errorMessage.value = "Something went wrong"
    }
  }
  loading.value = false;
};
</script>
<template>
  <form
    @submit.prevent="login"
    class="flex w-full md:w-4/5 lg:w-3/10 flex-col items-center gap-4 py-4 px-8 drop-shadow-xl bg-[var(--color-background)] xl:w-3/10 rounded-2xl"
  >
    <h1 class="text-xl font-bold!">{{ $t('auth.login') }}</h1>
    <FloatLabel variant="on" class="w-full">
      <InputText
        v-model="username"
        id="un_field"
        required="true"
        fluid
      />
      <label for="un_field">{{ $t('auth.username') }}</label>
    </FloatLabel>
    <FloatLabel variant="on" class="w-full">
      <Password
        v-model="password"
        id="ps_field"
        fluid
        :required="true"
        toggle-mask
        autocomplete="current-password"
        :feedback="false"
      />
      <label for="ps_field">{{ $t('auth.password') }}</label>
    </FloatLabel>
    <Button :loading="loading" :label="$t('auth.loginButton')" type="submit" fluid />
    <p class="text-red-700">{{ errorMessage }}</p>
  </form>
</template>
