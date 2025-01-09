import 'package:rxdart/rxdart.dart';

import 'custom_auth_manager.dart';

class GitpeekAuthUser {
  GitpeekAuthUser({required this.loggedIn, this.uid});

  bool loggedIn;
  String? uid;
}

/// Generates a stream of the authenticated user.
BehaviorSubject<GitpeekAuthUser> gitpeekAuthUserSubject =
    BehaviorSubject.seeded(GitpeekAuthUser(loggedIn: false));
Stream<GitpeekAuthUser> gitpeekAuthUserStream() => gitpeekAuthUserSubject
    .asBroadcastStream()
    .map((user) => currentUser = user);
