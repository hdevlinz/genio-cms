import { StatusCodes } from 'http-status-codes'
import { ofetch } from 'ofetch'
import { toast } from 'vue3-toastify'

export const $api = ofetch.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  async onRequest({ options }) {
    const accessToken = useCookie('accessToken').value
    if (accessToken) {
      options.headers = {
        ...options.headers,
        Authorization: `Bearer ${accessToken}`,
      }
    }
  },
  async onResponseError(context) {
    const { response } = context
    if (response?.status === StatusCodes.UNAUTHORIZED) {
      toast.error('Unauthorized access. Please login again.')
    }
    else if (response?.status === StatusCodes.FORBIDDEN) {
      toast.error('Access denied. You do not have permission to perform this action.')
    }
    else if (response?._data && response?._data?.errors) {
      const errorMessage = Array.isArray(response?._data?.errors)
        ? response?._data?.errors[0]
        : Object.values(response?._data?.errors)[0]

      toast.error(errorMessage)
    }
  },
})
