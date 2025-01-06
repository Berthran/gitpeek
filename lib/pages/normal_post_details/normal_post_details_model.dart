import '/flutter_flow/flutter_flow_util.dart';
import 'normal_post_details_widget.dart' show NormalPostDetailsWidget;
import 'package:flutter/material.dart';

class NormalPostDetailsModel extends FlutterFlowModel<NormalPostDetailsWidget> {
  ///  State fields for stateful widgets in this page.

  // State field(s) for TextField widget.
  final textFieldKey = GlobalKey();
  FocusNode? textFieldFocusNode;
  TextEditingController? textController;
  String? textFieldSelectedOption;
  String? Function(BuildContext, String?)? textControllerValidator;

  @override
  void initState(BuildContext context) {}

  @override
  void dispose() {
    textFieldFocusNode?.dispose();
  }
}
