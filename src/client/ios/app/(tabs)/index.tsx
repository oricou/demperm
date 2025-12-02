import { Redirect } from 'expo-router';
import {useUser} from "@/contexts/user-context";


export default function Index() {
  return <Redirect href="/auth/login" />;
}
