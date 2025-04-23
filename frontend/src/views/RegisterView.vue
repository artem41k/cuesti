<script setup>
import { registerUserReq } from "@/services/api";
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const username = ref("");
const password = ref("");
const confirmPassword = ref("");
const errorMessage = ref("");
const invalid = ref({
  username: false,
  password: false,
  confirmPassword: false,
});

const loading = ref(false);

const validate = () => {
  invalid.value.username = username.value ? false : true;
  invalid.value.password = password.value ? false : true;
  invalid.value.confirmPassword =
    password.value === confirmPassword.value ? false : true;
};

const isFormValid = computed(
  () =>
    !(
      invalid.value.username ||
      invalid.value.password ||
      invalid.value.confirmPassword
    ) &&
    username.value &&
    password.value
);

const register = async () => {
  if (password.value !== confirmPassword.value) {
    errorMessage.value = "Passwords must match";
    return;
  }
  loading.value = true;
  const data = { username: username.value, password: password.value };
  try {
    const response = await registerUserReq(data);
    router.push('/login');
  } catch (error) {
    if (error.response?.status === 400) {
      console.log(error.response.data);
      if (error.response.data?.username) {
        errorMessage.value = error.response.data.username[0];
      }
    } else {
      errorMessage.value = "Something went wrong";
    }
  }
  loading.value = false;
};
</script>
<template>
  <form
    @submit.prevent="register"
    class="flex w-full md:w-4/5 lg:w-3/10 flex-col items-center gap-4 py-4 px-8 drop-shadow-xl bg-[var(--color-background)] xl:w-3/10 rounded-2xl"
  >
    <h1 class="text-xl font-black">{{ $t('auth.register') }}</h1>
    <FloatLabel variant="on" class="w-full">
      <InputText
        v-model="username"
        id="un_field"
        fluid
        @input="validate"
        :invalid="invalid.username"
      />
      <label for="un_field">{{ $t('auth.username') }}</label>
    </FloatLabel>
    <FloatLabel variant="on" class="w-full">
      <Password
        v-model="password"
        input-id="ps_field"
        class="w-full"
        fluid
        @input="validate"
        :invalid="invalid.password"
        autocomplete="new-password"

        toggle-mask
        :prompt-label="$t('auth.enterPassword')"
        :weak-label="$t('auth.weakPassword')"
        :medium-label="$t('auth.mediumPassword')"
        :strong-label="$t('auth.strongPassword')"
      />
      <label for="ps_field">{{ $t('auth.password') }}</label>
    </FloatLabel>
    <FloatLabel variant="on" class="w-full">
      <Password
        v-model="confirmPassword"
        input-id="cp_field"
        class="w-full"
        fluid
        @input="validate"
        :invalid="invalid.confirmPassword"
        toggle-mask
        autocomplete="new-password"
        :feedback="false"
      />
      <label for="cp_field">{{ $t('auth.confirmPassword') }}</label>
    </FloatLabel>
    <Button
      :disabled="!isFormValid"
      :loading="loading"
      fluid
      type="submit"
      :label="$t('auth.registerButton')"
    />
    <p class="text-red-700">{{ errorMessage }}</p>
  </form>
</template>
