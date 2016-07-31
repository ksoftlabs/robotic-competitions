boolean isOnLine() {
  if (s5 == 0 && s6 == 0 && s7 == 1 && s8 == 0 && s9 == 0) {
    return true;
  }
  else {
    return false;
  }
}

boolean isOnLeft90() {
  if (s5 == 1 && s6 == 1 && s7 == 1 && s8 == 0 && s9 == 0) {
    return true;
  }
  else {
    return false;
  }
}

boolean isOnRight90() {
  if (s5 == 0 && s6 == 0 && s7 == 1 && s8 == 1 && s9 == 1) {
    return true;
  }
  else {
    return false;
  }
}

boolean isOnNode() {
  if (s5 == 1 && s6 == 1 && s7 == 0 && s8 == 1 && s9 == 1) {
    return true;
  }
  else {
    return false;
  }
}

boolean isOnBoundary() {
  if (s5 == 0 && s6 == 0 && s7 == 0 && s8 == 0 && s9 == 0) {
    return true;
  }
  else {
    return false;
  }
}

boolean isOnJunction() {
  if (s5 == 1 && s6 == 1 && s7 == 1 && s8 == 1 && s9 == 1) {
    return true;
  }
  else {
    return false;
  }
}

boolean isOnBlockBase() {
  if (s5 == 1 && s6 == 0 && s7 == 1 && s8 == 0 && s9 == 1) {
    return true;
  }
  else {
    return false;
  }
}
