import '/backend/api_requests/api_calls.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/form_field_controller.dart';
import 'choose_repository_widget.dart' show ChooseRepositoryWidget;
import 'package:flutter/material.dart';

class ChooseRepositoryModel extends FlutterFlowModel<ChooseRepositoryWidget> {
  ///  Local state fields for this page.

  List<String> apiRepoData = [];
  void addToApiRepoData(String item) => apiRepoData.add(item);
  void removeFromApiRepoData(String item) => apiRepoData.remove(item);
  void removeAtIndexFromApiRepoData(int index) => apiRepoData.removeAt(index);
  void insertAtIndexInApiRepoData(int index, String item) =>
      apiRepoData.insert(index, item);
  void updateApiRepoDataAtIndex(int index, Function(String) updateFn) =>
      apiRepoData[index] = updateFn(apiRepoData[index]);

  ///  State fields for stateful widgets in this page.

  // Stores action output result for [Backend Call - API (GetRepositories)] action in choose_repository widget.
  ApiCallResponse? apiResultpi6;
  // State field(s) for selectedRepository widget.
  String? selectedRepositoryValue;
  FormFieldController<String>? selectedRepositoryValueController;

  @override
  void initState(BuildContext context) {}

  @override
  void dispose() {}
}
