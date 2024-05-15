export interface User {
  id: number;
  pid: number;
  onyen: string;
  first_name: string;
  last_name: string;
  email: string;
  pronouns: string;
  github: string;
  github_id: string;
  github_avatar: string;
  permissions: string[];
  is_coworking: boolean;
}
