def in_square_brackets(string):
    return '['+string+']'


def in_curly_braces(string):
    return '{'+string+'}'


def tex_command(command_name, arguments=[], optional_arguments=[]):
    command = ['\{0}'.format(command_name)]

    for opt_arg in optional_arguments: 
        command.append(in_square_brackets(opt_arg))
    for arg in arguments: 
        command.append(in_curly_braces(arg))
    if len(arguments) == 0:
        command.append(in_curly_braces(''))
    return ''.join(command)


def tex_environment_begin(environment_name, arguments=[], optional_arguments=[]):
    environment = [tex_command('begin', [environment_name])]
    for opt_arg in optional_arguments: 
        environment.append(in_square_brackets(opt_arg))
    for arg in arguments: 
        environment.append(in_curly_braces(arg))
    return ''.join(environment)


def tex_environment_end(environment_name):
    return tex_command('end', [environment_name])


def tex_environment(environment_name, content=[], arguments=[], optional_arguments=[]):
    environment = [tex_environment_begin(environment_name, arguments, optional_arguments)]
    environment.append('\n')
    environment.extend(content)
    environment.append('\n')
    environment.append(tex_environment_end(environment_name))
    environment.append('\n')
    return ''.join(environment)
