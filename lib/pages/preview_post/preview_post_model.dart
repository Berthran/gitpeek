import '/flutter_flow/flutter_flow_util.dart';
import 'preview_post_widget.dart' show PreviewPostWidget;
import 'package:flutter/material.dart';

class PreviewPostModel extends FlutterFlowModel<PreviewPostWidget> {
  ///  Local state fields for this page.

  List<String> repoFiles = [];
  void addToRepoFiles(String item) => repoFiles.add(item);
  void removeFromRepoFiles(String item) => repoFiles.remove(item);
  void removeAtIndexFromRepoFiles(int index) => repoFiles.removeAt(index);
  void insertAtIndexInRepoFiles(int index, String item) =>
      repoFiles.insert(index, item);
  void updateRepoFilesAtIndex(int index, Function(String) updateFn) =>
      repoFiles[index] = updateFn(repoFiles[index]);

  bool showTextField = true;

  bool isTextField1Valid = true;

  ///  State fields for stateful widgets in this page.

  // State field(s) for TextField widget.
  final textFieldKey1 = GlobalKey();
  FocusNode? textFieldFocusNode1;
  TextEditingController? textController1;
  String? textFieldSelectedOption1;
  String? Function(BuildContext, String?)? textController1Validator;
  // State field(s) for TextField widget.
  final textFieldKey2 = GlobalKey();
  FocusNode? textFieldFocusNode2;
  TextEditingController? textController2;
  String? textFieldSelectedOption2;
  String? Function(BuildContext, String?)? textController2Validator;

  @override
  void initState(BuildContext context) {}

  @override
  void dispose() {
    textFieldFocusNode1?.dispose();

    textFieldFocusNode2?.dispose();
  }
}
