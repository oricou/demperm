export class DemocracySettings {
    shuwMyVote!: boolean;
    limitVotes!: boolean;
}

export class SocialSettings {
    public!: boolean;
}

export class Settings {
    democracy!: DemocracySettings;
    social!: SocialSettings;
}