import '/backend/api_requests/api_calls.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/form_field_controller.dart';
import 'normal_post_details_copy_widget.dart' show NormalPostDetailsCopyWidget;
import 'package:flutter/material.dart';

class NormalPostDetailsCopyModel
    extends FlutterFlowModel<NormalPostDetailsCopyWidget> {
  ///  Local state fields for this page.

  List<String> repoFiles = [];
  void addToRepoFiles(String item) => repoFiles.add(item);
  void removeFromRepoFiles(String item) => repoFiles.remove(item);
  void removeAtIndexFromRepoFiles(int index) => repoFiles.removeAt(index);
  void insertAtIndexInRepoFiles(int index, String item) =>
      repoFiles.insert(index, item);
  void updateRepoFilesAtIndex(int index, Function(String) updateFn) =>
      repoFiles[index] = updateFn(repoFiles[index]);

  ///  State fields for stateful widgets in this page.

  // Stores action output result for [Backend Call - API (GetFiles)] action in normalPostDetailsCopy widget.
  ApiCallResponse? apiResultoaa;
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
  // State field(s) for DropDown widget.
  List<String>? dropDownValue;
  FormFieldController<List<String>>? dropDownValueController;

  @override
  void initState(BuildContext context) {}

  @override
  void dispose() {
    textFieldFocusNode1?.dispose();

    textFieldFocusNode2?.dispose();
  }
}
