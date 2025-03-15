import { createFetch } from '@vueuse/core'
import { destr } from 'destr'
import { StatusCodes } from 'http-status-codes'
import { toast } from 'vue3-toastify'

interface ApiResponse {
  data: {
    id: number
    name: string
  }
}

export const useApi = createFetch({
  baseUrl: import.meta.env.VITE_API_BASE_URL || '/api',
  fetchOptions: {
    headers: {
      Accept: 'application/json',
    },
  },
  options: {
    refetch: true,
    async beforeFetch({ options }) {
      const accessToken = useCookie('accessToken').value

      if (accessToken) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${accessToken}`,
        }
      }

      return { options }
    },
    afterFetch(ctx) {
      const { data, response } = ctx

      if (response.status >= 400) {
        throw new Error(JSON.stringify({
          response,
          data: destr(data),
        }))
      }

      // Parse data if it's JSON
      let parsedData: unknown
      parsedData = null
      try {
        parsedData = destr(data)
      }
      catch (error) {
        console.error(error)
      }

      const typedData = parsedData as ApiResponse

      return { data: typedData.data, response }
    },
    updateDataOnError: true,
    onFetchError(ctx) {
      const { data, response, error } = ctx

      if (response?.status === StatusCodes.UNAUTHORIZED) {
        toast.error('Unauthorized access. Please login again.')
      }
      else if (response?.status === StatusCodes.FORBIDDEN) {
        toast.error('Access denied. You do not have permission to perform this action.')
      }
      else if (data && data.errors) {
        const errorMessage = Array.isArray(data.errors) ? data.errors[0] : Object.values(data.errors)[0]

        toast.error(errorMessage)
      }

      return { error, data, response }
    },
  },
})
