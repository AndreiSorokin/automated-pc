import { UserRole } from './UserRole';

export type User = {
  id: number;
  email: string;
  password: string;
  role: UserRole;
};
