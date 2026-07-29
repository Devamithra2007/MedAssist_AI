import { z } from "zod";

export const registerSchema = z
  .object({
    full_name: z.string().min(3, "Full name must be at least 3 characters"),

    email: z.string().email("Enter a valid email"),

    password: z.string().min(6, "Password must be at least 6 characters"),

    confirmPassword: z.string(),

    role: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
  });

export type RegisterFormData = z.infer<typeof registerSchema>;