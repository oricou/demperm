import { UserDto } from './user.dto';

export class UserProfileDto {
    profileId!: number;
    user!: UserDto;
    bio!: string;
    location!: string;
    createdAt!: Date;
    updatedAt!: Date;
}
