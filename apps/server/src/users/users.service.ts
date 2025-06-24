import { Injectable } from '@nestjs/common';
import * as bcrypt from 'bcrypt';
import { User } from 'types/User';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

@Injectable()
export class UsersService {
  constructor(
    // eslint-disable-next-line @typescript-eslint/no-unsafe-call
    @InjectRepository(User)
    private usersRepository: Repository<User>,
  ) {}

  async createUser(createUserDto: CreateUserDto): Promise<User> {
    const user = new User();
    user.firebaseUid = createUserDto.firebaseUid;
    user.email = createUserDto.email;
    user.password = await bcrypt.hash(createUserDto.password, 10);
    user.name = createUserDto.name;
    user.dateOfBirth = new Date(createUserDto.dateOfBirth);
    user.role = UserRole.ADMIN;
    user.instagram = createUserDto.instagram;
    user.telegram = createUserDto.telegram;
    user.resetToken = null;
    user.resetTokenExpiration = null;

    return this.usersRepository.save(user);
  }
}
